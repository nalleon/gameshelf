package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Format;

import java.util.List;

public interface IFormatRepository {
    Format save(Format format);
    List<Format> findAll();
    Format findById(Integer id);
    Format findByName(String name);
    boolean delete(Integer id);
    Format update(Format format);
}
